#!/usr/bin/env python3
"""R18: the stored flat-instance costs of X-005 (their C kernel, job M-008: `flat` of every cell of x005_cost.jsonl)
against my exact mean run (r18_mean.py), at sizes their Python reference cannot reach within 2 GB.

The flat instance is one atom (ln W = 0, psi0 = 0, place u n_i), so my run does not grow with n_o beyond the cube
tables.  Inner costs: their `alg2l.inner_costs` (a table of costs: input).  Their stored values were computed
before the tie rule of ENG-MSG-0003 §5; mine is exact arithmetic, i.e. the tie rule.  A difference is therefore
not necessarily an error of either; agreement is a replication.

usage: python3 -I -B r18_flat_large.py [--umax <u>] <n> [<n> ...] [--phi 0.5 ...]      (their code for the costs: use ulimit -v)
"""
import json, math, sys, time, resource
from fractions import Fraction as Fr
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "rerun_copy" / "src")); sys.path.insert(0, str(HERE / "rerun_copy" / "experiments" / "eng" / "twolevel")); sys.path.insert(0, str(HERE))
import mpmath as mp
import r18_mean as M
import run_search
from metricchain_eng.twolevel.alg2l import constants, inner_costs
from metricchain_eng.twolevel.tables import CubeTables
RES = Path("/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c/experiments/eng/twolevel/results")
args = sys.argv[1:]
umax = 1e9
if "--umax" in args:
    k = args.index("--umax")
    umax = float(args[k + 1])
    args = args[:k] + args[k + 2:]
phis = [0.5]
if "--phi" in args:
    k = args.index("--phi")
    phis = [float(x) for x in args[k + 1:]]
    args = args[:k]
ns = [int(x) for x in args]
t_all = time.time()
n_cmp = n_bad = 0
worst = 0.0
for line in (RES / "x005_cost.jsonl").read_text().splitlines():
    c = json.loads(line)
    if c["n"] not in ns or c["phi"] not in phis or c["u"] > umax:
        continue
    t = time.time()
    u_f, n, phi = c["u"], c["n"], c["phi"]
    P, _ = run_search.design_params(n, u_f, phi, c["design"])
    tabs = CubeTables(P.n_o, u_f)
    C = constants(P, tabs)
    lC = inner_costs(P, C)
    u = Fr(u_f)
    D = M.Design(n, P.n_o, u, Fr(1, 5), Fr(1, 20), 0.05, 0.05, P.nu1, Fr(1, 2), 0.05, [2 * u * P.n_i] + [Fr(x) for x in P.xs[1:-1]] + [Fr(1, 2)],
                 lC=[None] + [float(x) for x in lC[1:]])
    consts_ok = (D.J, D.K, D.r_dag, D.m_max) == (C.J, C.K, C.r_dag, C.m_max) == (c["constants"]["J"], c["constants"]["K"], c["constants"]["r_dag"], c["constants"]["m_max"])
    for orc in ("bottom", "top"):
        pos = M.uniform_positions(D, orc)
        R = M.mean_run(D, [(Fr(0), 1 << P.n_o, u * P.n_i, pos)], 1 << P.n_o, Fr(0), pop_tol=M.POP_TOL_THEIRS)
        st = c["flat"][orc]
        d = float(R.lcost) - st["lcost"]
        n_cmp += 1
        same = (R.j_stop == st["j_stop"] and abs(float(R.lM_max) - st["lM_max"]) < 1e-9 and abs(d) < 1e-8 * max(1.0, abs(st["lcost"])))
        n_bad += not same
        worst = max(worst, abs(d))
        print(f"u={u_f:g} n={n} phi={phi:.2f} flat {orc:6s}: mine ln cost {float(R.lcost):.9f} level {R.j_stop} ln M {float(R.lM_max):.6f} | stored {st['lcost']:.9f} level {st['j_stop']} ln M {st['lM_max']:.6f} "
              f"| difference {d:+.3e}  constants equal (mine, theirs, stored): {consts_ok}  {'AGREE' if same else 'DIFFERENT'}  ({time.time() - t:.0f} s)", flush=True)
print(f"compared {n_cmp}; different {n_bad}; largest |difference of ln cost| {worst:.3e}")
print(f"wall {time.time() - t_all:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")
