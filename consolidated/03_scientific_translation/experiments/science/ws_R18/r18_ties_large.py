#!/usr/bin/env python3
"""R18: ties at the ends of the refinement windows, at sizes of the published grid.

Their reference decides "level j is in the window" with a tolerance of 1e-12 in units of lambda on a quotient
computed in floats (meanrun.py l.435-436), while `ln s_j`, `ln W` carry rounding of the order of 1e-12 .. 1e-11 at
n = 2000 .. 16000.  Structural ties exist: with flat fibres (c_in = 0) and a profile on the level grid, the upper
end of the rung-0 window, W e^{x0 - t0} = W e^{u n_i}, is a level exactly.  Here: the X-005 design, u = 1 (u/lambda = 5),
profiles with integer slopes (cone up to a radius, then flat; flat), reference in the middle shell, flat fibres;
their reference against my exact mean run (r18_mean.py, their tolerance in "populated" reproduced).

usage: python3 -I -B r18_ties_large.py <n> [<n> ...]        (their code: use ulimit -v)
"""
import math, sys, time, resource
from fractions import Fraction as Fr
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "rerun_copy" / "src")); sys.path.insert(0, str(HERE))
import numpy as np
import mpmath as mp
import r18_mean as M
import r18_xcheck as X
from metricchain_eng.twolevel.alg2l import Params, constants, inner_costs, lC_max
from metricchain_eng.twolevel.tables import CubeTables

t0_ = time.time()
tot = dict(runs=0, bad=0, levels=0, closed=0)
for n in [int(x) for x in sys.argv[1:]] or [1000]:
    u, phi = Fr(1), 0.5
    n_o = int(math.floor(phi * n)); n_i = n - n_o
    eps = math.log(math.cosh(0.5))
    xs_f = [2.0 * n_i] + [eps * 0.85 ** i * n_i for i in range(40) if 0.5 < eps * 0.85 ** i * n_i < 2.0 * n_i] + [0.5]
    nu1 = max(1.0, 2 * math.exp(1.0) * n_o / 0.05)
    P = Params(n=n, n_o=n_o, u=1.0, lam=0.2, eta=0.05, etap=0.05, theta=0.05, nu1=nu1, b=0.5, delta=0.05, xs=tuple(xs_f))
    tabs = CubeTables(n_o, 1.0)
    C = constants(P, tabs); lC = inner_costs(P, C); lCmax_t = lC_max(P, C, lC)
    D = M.Design(n, n_o, u, Fr(1, 5), Fr(1, 20), 0.05, 0.05, nu1, Fr(1, 2), 0.05, [2 * u * n_i] + [Fr(x) for x in xs_f[1:-1]] + [Fr(1, 2)],
                 lC=[None] + [float(x) for x in lC[1:]])
    assert (D.J, D.K, D.r_dag, D.m_max) == (C.J, C.K, C.r_dag, C.m_max)
    for name, F in (("flat", [Fr(0)] * (n_o + 1)), ("cone to 0.3 n_o, then flat", [u * min(d, int(0.3 * n_o)) for d in range(n_o + 1)]),
                    ("cone to 0.4 n_o, then flat", [u * min(d, int(0.4 * n_o)) for d in range(n_o + 1)])):
        d0 = n_o // 2
        for orc in ("bottom", "top"):
            pos = M.uniform_positions(D, orc)
            atoms, den = M.radial_atoms(D, F, 0, pos=pos)                     # c_in = 0: flat fibres, place u n_i
            t = time.time()
            Rm = M.mean_run(D, atoms, den, F[d0], pop_tol=M.POP_TOL_THEIRS)
            tm = time.time() - t
            Rt = X.their_run(P, tabs, C, lC, [float(x) for x in F], 0.0, float(F[d0]), float(u * n_i), orc)
            ok = X.compare(f"n={n} {name} {orc}", Rm, Rt, D, P, C, lCmax_t, tot, True)
            # ties actually present at the upper end of the rung-0 window: atoms with (lnW + u n_i - ln s0)/lambda an integer <= j_stop
            ties = sum(1 for (lw, wt, t0, _) in atoms if ((lw + u * n_i - Rm.ls0) / D.lam).denominator == 1 and (lw + u * n_i - Rm.ls0) / D.lam <= Rm.j_stop)
            print(f"n={n} n_o={n_o} {name:28s} {orc:6s}: level {Rm.j_stop}, m {Rm.m_top}; atoms with the rung-0 window ending exactly on a level <= j_stop: {ties} of {len(atoms)}; "
                  f"ln cost mine {float(Rm.lcost):.9f} theirs {Rt.lcost:.9f}; ln calls of I_1 mine {float(Rm.lcalls[1]):.9f} theirs {float(Rt.lcalls[1]):.9f}; "
                  f"{'AGREE' if ok else 'MISMATCH'}  (my run {tm:.0f} s)", flush=True)
print(f"runs {tot['runs']}, mismatches {tot['bad']}, levels compared {tot['levels']}")
print(f"wall {time.time() - t0_:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")
