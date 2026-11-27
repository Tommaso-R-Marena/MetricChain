#!/usr/bin/env python3
"""R18, item 3 -- is "uniform inner behaviour" needed for the bound of ENG-RES-0014 §4?

The message says the bound does not cover "inner behaviours that differ from point to point (a point in the
tolerance zone can be made HIGH or LOW by where its bracket is put, which changes the sample sizes, not only the
calls)".  Here: a search for an instance, with the SAME law of fibre averages and the same reference value, in
which the inner behaviour ("bottom" or "top") and the place (lo or hi) depend on the outer shell, and whose
mean-run cost exceeds

    target = max( placement-free bound with "bottom" for all , placement-free bound with "top" for all ).

If such an instance is found, the restriction to uniform behaviours is essential for the bound (class F of the
assumption audit, with the instance as the counterexample); if none is found, nothing is established.

Search: (1) thresholds -- "top" for the shells with ln W above a threshold and "bottom" below, and the reverse,
each with places lo/hi/product; (2) coordinate ascent over the shells from the best start.
Mean runs: r18_mean.py (mine).  Inner costs: an input; `--costs theirs` takes ln C_l of the base family from the
engineering division's `alg2l.inner_costs` (their code, used as a table of costs only), `--costs toy` uses 2 + 3l.

usage: python3 -I -B r18_mixed.py [--costs theirs|toy] [n u phi profile] ...
"""
import math
import resource
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mpmath as mp                                                             # noqa: E402

import r18_mean as M                                                            # noqa: E402
from r18_nonproduct import lam1                                                 # noqa: E402


CAP = 100.0          # seconds of search per case (coordinate ascent stops there)


def their_costs(n, n_o, u, xs_f):
    sys.path.insert(0, str(HERE / "rerun_copy" / "src"))
    from metricchain_eng.twolevel.alg2l import Params, constants, inner_costs
    from metricchain_eng.twolevel.tables import CubeTables
    P = Params(n=n, n_o=n_o, u=u, lam=0.2, eta=0.05, etap=0.05, theta=0.05, nu1=max(1.0, 2 * math.exp(u) * n_o / 0.05), b=0.5, delta=0.05, xs=tuple(xs_f))
    C = constants(P, CubeTables(n_o, u))
    return [None] + [float(x) for x in inner_costs(P, C)[1:]], (C.J, C.K, C.r_dag, C.m_max)


def design(n, u, phi, costs):
    n_o = max(1, min(n - 1, int(math.floor(phi * n))))
    n_i = n - n_o
    eps = math.log(math.cosh(float(u) / 2))
    xs_f = [2 * float(u) * n_i] + [eps * 0.85 ** i * n_i for i in range(40) if 0.5 < eps * 0.85 ** i * n_i < 2 * float(u) * n_i] + [0.5]
    xs = [2 * u * n_i] + [Fr(x) for x in xs_f[1:-1]] + [Fr(1, 2)]
    if costs == "theirs":
        lC, consts = their_costs(n, n_o, float(u), xs_f)
    else:
        lC, consts = [None] + [2.0 + 3.0 * l for l in range(1, len(xs))], None
    D = M.Design(n, n_o, u, Fr(1, 5), Fr(1, 20), 0.05, 0.05, max(1.0, 2 * math.exp(float(u)) * n_o / 0.05), Fr(1, 2), 0.05, xs, lC=lC)
    if consts is not None:
        assert consts == (D.J, D.K, D.r_dag, D.m_max), (consts, (D.J, D.K, D.r_dag, D.m_max))
    return D


def profile(name, u, n_o):
    if name == "flat":
        return [Fr(0)] * (n_o + 1)
    if name == "cone":
        return [u * d for d in range(n_o + 1)]
    if name.startswith("dip"):                       # cone below a radius, flat above
        R = int(float(name[3:]) * lam1(u) / float(u) * n_o)
        return [u * min(d, R) for d in range(n_o + 1)]
    if name.startswith("plateau"):                   # flat below a radius, cone above
        R = int(float(name[7:]) * n_o)
        return [u * max(d - R, 0) for d in range(n_o + 1)]
    raise ValueError(name)


def search(n, u, phi, prof, costs):
    t_start = time.time()
    D = design(n, u, phi, costs)
    n_o, n_i = D.n_o, D.n_i
    L1 = lam1(u)
    lo, hi = Fr(n_i * (float(u) - L1)), Fr(n_i * (2 * float(u) - L1))
    F = profile(prof, u, n_o)
    d0 = n_o // 2
    psi0 = F[d0]
    c_in = Fr(0)                                      # flat fibres at the reference: place u n_i
    t_ref = u * n_i + c_in
    POS = {"B": M.uniform_positions(D, "bottom"), "T": M.uniform_positions(D, "top")}
    lnW = [c_in - F[d] for d in range(n_o + 1)]
    binom = D.cube.binom
    den = 1 << n_o
    nrun = [0]

    def cost(assign, union=None):
        nrun[0] += 1
        at = [(lnW[d], binom[d], assign[d][1], POS[assign[d][0]]) for d in range(n_o + 1)]
        R = M.mean_run(D, at, den, psi0, union=union)
        return R.lcost if R.status.startswith("closed") else -mp.inf, R

    uni = {}
    for beh in "BT":
        c_prod, Rp = cost([(beh, t_ref)] * (n_o + 1))
        c_bound, Rb = cost([(beh, t_ref)] * (n_o + 1), union=(lo, hi))
        uni[beh] = (c_prod, c_bound, Rp.j_stop, Rp.m_top)
    target = max(uni["B"][1], uni["T"][1])
    # (1) thresholds on the rank of ln W
    order = sorted(range(n_o + 1), key=lambda d: (lnW[d], d))
    best, best_assign, best_tag = -mp.inf, None, ""
    cuts = sorted(set(list(range(0, n_o + 2, max(1, (n_o + 1) // 24))) + [n_o + 1]))
    for upper, lower in (("T", "B"), ("B", "T")):
        for pl_name, pu, pl in (("ref", t_ref, t_ref), ("hi above / lo below", hi, lo), ("lo above / hi below", lo, hi)):
            for k in cuts:
                assign = [None] * (n_o + 1)
                for r, d in enumerate(order):
                    assign[d] = (upper, pu) if r >= k else (lower, pl)
                c, _ = cost(assign)
                if c > best:
                    best, best_assign, best_tag = c, assign, f"{upper} for the {n_o + 1 - k} shells of largest W, {lower} below; places {pl_name}"
    after_thresholds = best
    # (2) coordinate ascent over the shells that carry weight or sit in the tails near the stopping level
    opts = [("B", lo), ("B", hi), ("T", lo), ("T", hi)]
    improved = True
    sweeps = 0
    while improved and sweeps < 2 and time.time() - t_start < CAP:
        improved = False
        sweeps += 1
        for d in sorted(range(n_o + 1), key=lambda d: -binom[d]):
            cur = best_assign[d]
            for o in opts:
                if o == cur:
                    continue
                trial = list(best_assign)
                trial[d] = o
                c, _ = cost(trial)
                if c > best + mp.mpf(10) ** (-12):
                    best, best_assign, improved = c, trial, True
                    best_tag = "coordinate ascent"
            if time.time() - t_start > CAP:
                break
    cb, Rbest = cost(best_assign)
    nT = sum(1 for a in best_assign if a[0] == "T")
    print(f"n={n} u={float(u):g} phi={phi} profile={prof} costs={costs}: n_o={n_o} n_i={n_i} L={D.L} K={D.K}  ({nrun[0]} mean runs, {time.time() - t_start:.0f} s)")
    for beh, name in (("B", "bottom"), ("T", "top")):
        print(f"   uniform {name:6s}: product ln cost {float(uni[beh][0]):.6f} (level {uni[beh][2]}, m {uni[beh][3]});  placement-free bound {float(uni[beh][1]):.6f}")
    print(f"   target = max of the two bounds = {float(target):.6f};  ln C_max = {float(D.lCmax):.6f}")
    print(f"   best shell-dependent behaviour found: ln cost {float(cb):.6f} (level {Rbest.j_stop}, m {Rbest.m_top}; 'top' on {nT} of {n_o + 1} shells; after thresholds {float(after_thresholds):.6f}; {best_tag})")
    print(f"   EXCESS over the target: {float(cb - target):+.6f}   ({'the bound is EXCEEDED by an instance with point-dependent behaviour' if cb > target + mp.mpf(10) ** (-6) else 'not exceeded (within 1e-6)'}); "
          f"below C_max: {bool(cb <= D.lCmax)}", flush=True)
    return float(cb - target)


if __name__ == "__main__":
    args = sys.argv[1:]
    costs = "toy"
    if args and args[0] == "--costs":
        costs = args[1]
        args = args[2:]
    cases = []
    while args:
        cases.append((int(args[0]), Fr(args[1]), float(args[2]), args[3]))
        args = args[4:]
    if not cases:
        cases = [(100, Fr(1), 0.5, "flat"), (100, Fr(1), 0.5, "dip1.1"), (100, Fr(1), 0.7, "cone")]
    t = time.time()
    print(f"r18_mixed.py costs={costs} start {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}", flush=True)
    ex = [search(n, u, phi, prof, costs) for (n, u, phi, prof) in cases]
    print(f"cases {len(ex)}; with the target exceeded by more than 1e-6: {sum(e > 1e-6 for e in ex)}; largest excess {max(ex):+.6f}")
    print(f"end {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  wall {time.time() - t:.1f} s  peak RSS MB: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.1f}")
